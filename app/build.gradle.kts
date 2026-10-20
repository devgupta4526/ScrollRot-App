plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.scrollrot.app"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.scrollrot.app"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }
    buildTypes {
        release { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { viewBinding = true }
}
// Deliberately minimal: the starter uses built-in Android animations and storage.
// Follow BUILD_SPEC.md for the production MVVM/Room/Lottie/Firebase stack.
