plugins {
    kotlin("jvm") version "2.1.10"
    kotlin("plugin.serialization") version "2.1.10"
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

val ktor_version: String by project
val logback_version: String by project
val okhttp_version: String by project
val kord_version: String by project
val dotenv_version: String by project

dependencies {
    implementation("io.ktor:ktor-client-core:$ktor_version")
    implementation("io.ktor:ktor-client-cio:$ktor_version")
    implementation("ch.qos.logback:logback-classic:$logback_version")
    implementation("com.squareup.okhttp3:okhttp:$okhttp_version")
    implementation("io.ktor:ktor-client-content-negotiation:$ktor_version")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktor_version")
    implementation("io.github.cdimascio:dotenv-kotlin:$dotenv_version")
    implementation("dev.kord:kord-core:$kord_version")
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}