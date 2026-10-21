package com.scrollrot.app.ui

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.scrollrot.app.R
import com.scrollrot.app.store.TrackingStore

/**
 * Scroll Battle fragment matching BrainPal Image 3.
 * Features private friend leaderboards, invite slots, and challenge join code entry.
 */
class BattleFragment : Fragment() {

    private lateinit var store: TrackingStore
    private lateinit var battleYouCount: TextView
    private lateinit var inputJoinCode: EditText
    private lateinit var btnJoinBattle: Button

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_battle, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        store = TrackingStore(requireContext().applicationContext)

        battleYouCount = view.findViewById(R.id.battleYouCount)
        inputJoinCode = view.findViewById(R.id.inputJoinCode)
        btnJoinBattle = view.findViewById(R.id.btnJoinBattle)

        battleYouCount.text = store.total().toString()

        setupInviteButtons(view)

        btnJoinBattle.setOnClickListener {
            val code = inputJoinCode.text.toString().trim()
            if (code.length == 6) {
                Toast.makeText(requireContext(), "Joined Battle #$code! Leaderboard synced.", Toast.LENGTH_LONG).show()
                inputJoinCode.text.clear()
            } else {
                Toast.makeText(requireContext(), "Please enter a valid 6-digit challenge code", Toast.LENGTH_SHORT).show()
            }
        }

        view.findViewById<View>(R.id.btnFriends)?.setOnClickListener {
            AlertDialog.Builder(requireContext())
                .setTitle("Scrollrot Friends")
                .setMessage("Compete privately with your friends. Add friends by email or invite them with your unique challenge link.\n\nScores are self-reported daily aggregates; no personal videos, messages, or screen data are ever shared.")
                .setPositiveButton("Invite a Friend") { _, _ -> shareInvite("friend") }
                .setNegativeButton("Close", null)
                .show()
        }
    }

    private fun setupInviteButtons(v: View) {
        val inviteAction = View.OnClickListener {
            shareInvite("challenge")
        }

        v.findViewById<View>(R.id.btnInvite1)?.setOnClickListener(inviteAction)
        v.findViewById<View>(R.id.btnInvite2)?.setOnClickListener(inviteAction)
        v.findViewById<View>(R.id.btnInvite3)?.setOnClickListener(inviteAction)
        v.findViewById<View>(R.id.btnInvite4)?.setOnClickListener(inviteAction)
    }

    private fun shareInvite(inviteCategory: String) {
        val inviteCode = "82" + (1000..9999).random()
        val text = "Join my Scrollrot detox battle to see who doomscrolls less reels! Enter code: $inviteCode https://scrollrot.app/join/$inviteCode"
        val sendIntent = Intent().apply {
            action = Intent.ACTION_SEND
            putExtra(Intent.EXTRA_TEXT, text)
            this.type = "text/plain"
        }
        startActivity(Intent.createChooser(sendIntent, "Invite to Scroll Battle"))
    }

    fun refresh() {
        if (::battleYouCount.isInitialized) {
            battleYouCount.text = store.total().toString()
        }
    }
}
