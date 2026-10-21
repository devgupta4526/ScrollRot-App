package com.scrollrot.app.store

import android.content.Context
import android.os.Handler
import android.os.Looper
import java.time.LocalDate

/**
 * Thread-safe local tracking store managing daily platform counts,
 * preferences, and change notifications.
 */
class TrackingStore(context: Context) {
    private val prefs = context.getSharedPreferences("scrollrot_storage", Context.MODE_PRIVATE)
    private val platforms = listOf("instagram", "youtube", "facebook", "snapchat")
    private val mainHandler = Handler(Looper.getMainLooper())
    private val listeners = mutableListOf<() -> Unit>()

    fun addChangeListener(listener: () -> Unit) {
        synchronized(listeners) {
            listeners.add(listener)
        }
    }

    fun removeChangeListener(listener: () -> Unit) {
        synchronized(listeners) {
            listeners.remove(listener)
        }
    }

    private fun notifyChanged() {
        val copy = synchronized(listeners) { listeners.toList() }
        mainHandler.post {
            for (listener in copy) {
                listener.invoke()
            }
        }
    }

    @Synchronized
    private fun todayReady() {
        val key = LocalDate.now().toString()
        if (prefs.getString("day", null) != key) {
            val edit = prefs.edit().putString("day", key)
            for (platform in platforms) {
                edit.putInt(platform, 0)
            }
            edit.apply()
        }
    }

    @Synchronized
    fun add(platform: String) {
        todayReady()
        if (platform !in platforms) return
        val current = prefs.getInt(platform, 0)
        prefs.edit().putInt(platform, current + 1).apply()
        notifyChanged()
    }

    @Synchronized
    fun count(platform: String): Int {
        todayReady()
        return prefs.getInt(platform, 0)
    }

    @Synchronized
    fun total(): Int = platforms.sumOf { count(it) }

    fun consented(): Boolean = prefs.getBoolean("consent", false)
    fun saveConsent() { prefs.edit().putBoolean("consent", true).apply() }

    fun isFloatingHudEnabled(): Boolean = prefs.getBoolean("floating_hud_enabled", true)
    fun setFloatingHudEnabled(enabled: Boolean) {
        prefs.edit().putBoolean("floating_hud_enabled", enabled).apply()
        notifyChanged()
    }

    fun dailyGoal(): Int = prefs.getInt("daily_goal", 100)
    fun setDailyGoal(goal: Int) {
        prefs.edit().putInt("daily_goal", goal).apply()
        notifyChanged()
    }

    fun streakDays(): Int = prefs.getInt("streak_days", 4)
}
