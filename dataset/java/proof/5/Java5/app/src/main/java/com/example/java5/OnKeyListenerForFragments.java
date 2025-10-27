package com.example.java5;

import android.app.Fragment;


/**
 * Interface for fragments that want to handle key events from the activity
 */
public abstract class OnKeyListenerForFragments extends Fragment {
    public abstract void onKeyUp(int keyCode);
}
