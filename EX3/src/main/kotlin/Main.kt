package org.example

import dev.kord.core.Kord
import dev.kord.core.event.message.MessageCreateEvent
import dev.kord.core.on
import dev.kord.gateway.Intent
import dev.kord.gateway.PrivilegedIntent
import io.github.cdimascio.dotenv.dotenv
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json


@Serializable
data class DiscordMessage(val content: String)

suspend fun sendDiscordMessage(client: HttpClient, content: String, webhook: String) {
    val response: HttpResponse = client.post(webhook) {
        contentType(ContentType.Application.Json)
        setBody(DiscordMessage(content))
    }
    println("Status: ${response.status}")
}

@OptIn(PrivilegedIntent::class)
suspend fun main() {
    val dotenv = dotenv()
    val DISCORD_BOT_TOKEN = dotenv["DISCORD_BOT_TOKEN"]
    val DISCORD_WEBHOOK = dotenv["DISCORD_WEBHOOK"]

    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
    }
    sendDiscordMessage(client, "Hello from **Ktor** 🚀!", DISCORD_WEBHOOK)

    val kord = Kord(DISCORD_BOT_TOKEN)
    kord.on<MessageCreateEvent> {
        println("DEBUG: ${message.content}")
        if (message.content == "Ping!") {
            message.channel.createMessage("Pong!")
        }
    }
    kord.login { intents += Intent.MessageContent};
    client.close()
}
