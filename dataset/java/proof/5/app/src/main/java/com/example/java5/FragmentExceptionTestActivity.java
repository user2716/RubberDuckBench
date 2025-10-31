package com.example.java5;

import android.app.Activity;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

/**
 * Test Activity focused on testing the following scenarios:
 * 1. ClassCastException when casting to OnKeyListenerForFragments
 * 2. NPE prevention (null safety)
 * 3. IllegalStateException during irrelevant fragment operations
 */
public class FragmentExceptionTestActivity extends Activity {
    private static final String TAG = "FragmentExceptionTest";
    private TextView resultText;
    private int testNumber = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test);
        resultText = findViewById(R.id.result_text);
        
        // Run all tests
        runAllTests();
    }

    private void runAllTests() {
        log("=== Starting Fragment Exception Tests ===\n");

        // Test 1: ClassCastException (wrong fragment type)
        testClassCastException();

        //Test 2: ClassCastException when the fragment is not found
        testFragmentNotFound();

        // Test 3: IllegalStateException (fragment after onSaveInstanceState)
        testIllegalStateException();
        
        log("\n=== All Tests Complete ===");
    }

    /**
     * Test 1: Verify ClassCastException can occur with wrong fragment type
     */
    private void testClassCastException() {
        testNumber++;
        log("\nTest " + testNumber + ": ClassCastException (wrong fragment type)");

        try {
            // Add a fragment that does NOT implement OnKeyListenerForFragments
            WrongFragment wrongFragment = new WrongFragment();
            FragmentManager fm = getFragmentManager();
            FragmentTransaction transaction = fm.beginTransaction();
            transaction.replace(R.id.fragment_container, wrongFragment);
            transaction.commit();
            fm.executePendingTransactions(); // Execute immediately

            // Try to cast it (this should throw ClassCastException)
            OnKeyListenerForFragments myFragment =
                    (OnKeyListenerForFragments) getFragmentManager()
                            .findFragmentById(R.id.fragment_container);

        } catch (ClassCastException e) {
            log("ClassCastException caught: " + e.getMessage());
            // Clean uthe wrong fragment
            getFragmentManager().beginTransaction()
                    .remove(getFragmentManager().findFragmentById(R.id.fragment_container))
                    .commit();
        }
    }


    /**
     * Test 2: Verify ClassCast also occurs when fragment is null
     */
    private void testFragmentNotFound() {
        testNumber++;
        log("\nTest " + testNumber + ": ClassCastException occurs when fragment is not found");
        
        try {

            //Using a fragment that does not exist in the XML does not compile
            /*
                OnKeyListenerForFragments myFragment =
                   (OnKeyListenerForFragments) getFragmentManager()
                           .findFragmentById(R.id.some_other_fragment);
            */

            //Setting a fragment to null throws an NPE
            /*
            getFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, null)  // NPE!
                    .commit();
             */

            //this fragment exists, but is not yet added to the container
            OnKeyListenerForFragments myFragment =
                    (OnKeyListenerForFragments) getFragmentManager()
                            .findFragmentById(R.id.fragment_container);

            log("No exception when fragment is not found");
        } catch (ClassCastException e) {
            log("ClassCastException occurred: " + e.getMessage());
        }
    }

    /**
     * Test 3: Demonstrate IllegalStateException scenario
     */
    private void testIllegalStateException() {
        testNumber++;
        log("\nTest " + testNumber + ": IllegalStateException occurs when commiting a fragment transaction after the activity has saved its state");
        
        try {
            // Simulate onSaveInstanceState being called
            Bundle outState = new Bundle();
            onSaveInstanceState(outState);
            
            // Now try to commit a fragment transaction after onSaveInstanceState
            FeedItemListFragment fragment = new FeedItemListFragment();
            FragmentManager fm = getFragmentManager();
            FragmentTransaction transaction = fm.beginTransaction();
            transaction.replace(R.id.fragment_container, fragment);
            transaction.commit(); // This will throw IllegalStateException
            
        } catch (IllegalStateException e) {
            log("IllegalStateException caught in code unrelated to retrieving the fragment and casting it: " + e.getMessage());
        }
    }

    private void log(String message) {
        Log.d(TAG, message);
        if (resultText != null) {
            resultText.append(message + "\n");
        }
    }

    /**
     * Fragment that does NOT implement OnKeyListenerForFragments
     * Used to test ClassCastException
     */
    public static class WrongFragment extends Fragment {
        // This fragment intentionally does NOT implement OnKeyListenerForFragments
    }
}
