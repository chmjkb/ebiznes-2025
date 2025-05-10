package org.example

import io.ktor.http.HttpHeaders
import io.ktor.http.HttpMethod
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.request.receive
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*

@Serializable
data class Product(val id: Int, val name: String, val description: String, val price: Double)

@Serializable
data class PaymentRequest(
        val cardNumber: String,
        val cardHolder: String,
        val expirationDate: String,
        val cvv: String,
        val amount: Double,
)

val products =
        listOf(
                Product(1, "Laptop", "A fast laptop", 4900.99),
                Product(2, "Mouse", "Wireless mouse", 29.99),
                Product(3, "Keyboard", "Mechanical keyboard", 79.99)
        )

fun main() {
    embeddedServer(Netty, port = 8080) {
        install(ContentNegotiation) { json() }
        install(CORS) {
            // Allow all origins
            anyHost()

            allowMethod(HttpMethod.Get)
            allowMethod(HttpMethod.Post)
            allowHeader(HttpHeaders.ContentType)
        }

        routing {
            get("/products") { call.respond(products) }
            post("/payments") {
                val payment = call.receive<PaymentRequest>()
                println("Received payment: $payment")
                call.respond(mapOf("status" to "Payment received"))
            }
        }
    }
            .start(wait = true)
            .also { println("Server is running at http://localhost:8080") }
}
