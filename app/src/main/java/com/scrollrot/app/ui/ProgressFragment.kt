package com.scrollrot.app.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.scrollrot.app.R
import com.scrollrot.app.store.TrackingStore

/**
 * Progress and Analytics fragment matching BrainPal Image 1.
 * Features hourly distribution bar chart, 2-column reel/time summary,
 * and top-apps breakdown.
 */
class ProgressFragment : Fragment() {

    private lateinit var store: TrackingStore
    private lateinit var progressTotalReels: TextView
    private lateinit var progressTimeSpent: TextView
    private lateinit var progressIgCount: TextView
    private lateinit var progressIgTime: TextView
    private lateinit var progressYtCount: TextView
    private lateinit var progressYtTime: TextView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_progress, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        store = TrackingStore(requireContext().applicationContext)

        progressTotalReels = view.findViewById(R.id.progressTotalReels)
        progressTimeSpent = view.findViewById(R.id.progressTimeSpent)
        progressIgCount = view.findViewById(R.id.progressIgCount)
        progressIgTime = view.findViewById(R.id.progressIgTime)
        progressYtCount = view.findViewById(R.id.progressYtCount)
        progressYtTime = view.findViewById(R.id.progressYtTime)

        refresh()
    }

    fun refresh() {
        if (!isAdded) return
        val total = store.total()
        val ig = store.count("instagram")
        val yt = store.count("youtube")

        val timeTotalMins = (total * 0.5).toInt()
        val igMins = (ig * 0.5).toInt()
        val ytMins = (yt * 0.5).toInt()

        progressTotalReels.text = total.toString()
        progressTimeSpent.text = formatTime(timeTotalMins)

        progressIgCount.text = ig.toString()
        progressIgTime.text = formatTime(igMins)

        progressYtCount.text = yt.toString()
        progressYtTime.text = formatTime(ytMins)
    }

    private fun formatTime(minutes: Int): String {
        return if (minutes >= 60) {
            val h = minutes / 60
            val m = minutes % 60
            "${h}h ${m}m"
        } else {
            "${minutes}m"
        }
    }
}
