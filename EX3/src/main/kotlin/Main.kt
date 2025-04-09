package org.example

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

const val DISCORD_WEBHOOK = ""

@Serializable
data class DiscordMessage(val content: String)

suspend fun main() {
    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
    }

    val response: HttpResponse = client.post(DISCORD_WEBHOOK) {
        contentType(ContentType.Application.Json)
        setBody(DiscordMessage("Hello from **Ktor** 🚀"))
    }

    println("Status: ${response.status}")
    client.close()
}
