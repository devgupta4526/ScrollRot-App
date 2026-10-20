package com.scrollrot.app.store

import android.content.Context
import java.time.LocalDate

/** Prototype storage. Replace with Room + DataStore before a public launch. */
class TrackingStore(context: Context) {
    private val prefs = context.getSharedPreferences("scrollrot_demo", Context.MODE_PRIVATE)
    private val platforms = listOf("instagram", "youtube", "facebook", "snapchat")

    @Synchronized private fun todayReady() {
        val key = LocalDate.now().toString()
        if (prefs.getString("day", null) != key) {
            val edit = prefs.edit().clear().putString("day", key)
            // Preserve consent across midnight. Tracking service opt-in remains governed by Android.
            edit.putBoolean("consent", prefs.getBoolean("consent", false))
            edit.commit()
        }
    }

    @Synchronized fun add(platform: String) {
        todayReady()
        if (platform !in platforms) return
        prefs.edit().putInt(platform, prefs.getInt(platform, 0) + 1).apply()
    }

    @Synchronized fun count(platform: String): Int {
        todayReady()
        return prefs.getInt(platform, 0)
    }

    @Synchronized fun total(): Int = platforms.sumOf { count(it) }

    fun consented(): Boolean = prefs.getBoolean("consent", false)
    fun saveConsent() { prefs.edit().putBoolean("consent", true).apply() }
}
