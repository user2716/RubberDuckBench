package com.example.java5;

import android.os.Bundle;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.util.Log;

/**
 * Test fragment that implements OnKeyListenerForFragments interface
 */
public class FeedItemListFragment extends OnKeyListenerForFragments {
    private static final String TAG = "ItemListFragment";
    private TextView fragmentStatus;
    private int keyPressCount = 0;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_test, container, false);
        fragmentStatus = view.findViewById(R.id.fragment_status);
        updateStatus("Fragment ready");
        return view;
    }

    @Override
    public void onKeyUp(int keyCode) {
        keyPressCount++;
        String keyName = KeyEvent.keyCodeToString(keyCode);
        String message = String.format("Fragment received key: %s (count: %d)", 
                                       keyName, keyPressCount);
        Log.d(TAG, message);
        updateStatus(message);
    }

    private void updateStatus(String message) {
        if (fragmentStatus != null) {
            fragmentStatus.setText(message);
        }
    }
}
