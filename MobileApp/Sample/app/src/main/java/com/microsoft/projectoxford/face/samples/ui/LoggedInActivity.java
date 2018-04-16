package com.microsoft.projectoxford.face.samples.ui;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import com.microsoft.projectoxford.face.samples.R;

public class LoggedInActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged_in);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        SharedPreferences prefs = getSharedPreferences("personal", MODE_PRIVATE);
        String personId = prefs.getString("PersonId", null);
        if( personId == null){
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        }

    }


    public void changeAdsOnClick(View view) {
        Intent intent = new Intent(this, AdPrefsActivity.class);
        startActivity(intent);
    }

    public void changeIOTA(View view) {
        Intent intent = new Intent(this, SetupWalletActivity.class);
        startActivity(intent);
    }

    public void changePersonalOnClick(View view) {
        Intent intent = new Intent(this, UserDetailsActivity.class);
        startActivity(intent);
    }
}
