package com.scrollrot.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.scrollrot.app.store.TrackingStore
import com.scrollrot.app.ui.BattleFragment
import com.scrollrot.app.ui.DashboardFragment
import com.scrollrot.app.ui.ProgressFragment

/**
 * Main Activity shell hosting the 3 core navigation tabs:
 * 1. "You" (DashboardFragment)
 * 2. "Battle" (BattleFragment)
 * 3. "Progress" (ProgressFragment)
 *
 * Direct match for the BrainPal competition UI/UX architecture.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var store: TrackingStore
    private lateinit var bottomNav: BottomNavigationView

    private val dashboardFragment by lazy { DashboardFragment() }
    private val battleFragment by lazy { BattleFragment() }
    private val progressFragment by lazy { ProgressFragment() }

    private var activeFragment: Fragment = dashboardFragment

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        store = TrackingStore(applicationContext)
        bottomNav = findViewById(R.id.bottomNavigation)

        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction()
                .add(R.id.fragmentContainer, dashboardFragment, "YOU")
                .commit()
        }

        setupBottomNavigation()
    }

    private fun setupBottomNavigation() {
        bottomNav.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_you -> {
                    switchFragment(dashboardFragment)
                    true
                }
                R.id.nav_battle -> {
                    switchFragment(battleFragment)
                    true
                }
                R.id.nav_progress -> {
                    switchFragment(progressFragment)
                    true
                }
                else -> false
            }
        }
    }

    private fun switchFragment(target: Fragment) {
        if (target == activeFragment) return

        val transaction = supportFragmentManager.beginTransaction()

        if (!target.isAdded) {
            transaction.hide(activeFragment).add(R.id.fragmentContainer, target).commit()
        } else {
            transaction.hide(activeFragment).show(target).commit()
        }

        activeFragment = target

        // Trigger UI refresh on switch
        when (target) {
            is DashboardFragment -> target.refresh()
            is BattleFragment -> target.refresh()
            is ProgressFragment -> target.refresh()
        }
    }
}
