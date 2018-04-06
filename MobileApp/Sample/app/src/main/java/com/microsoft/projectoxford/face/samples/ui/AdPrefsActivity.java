package com.microsoft.projectoxford.face.samples.ui;
import com.microsoft.projectoxford.face.samples.R;
import com.microsoft.projectoxford.face.samples.helper.AdPrefsAdapter;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.ListView;

import java.util.HashMap;

public class AdPrefsActivity extends AppCompatActivity {
    private final HashMap<String, Float> ad_map = new HashMap<>();
    private AdPrefsAdapter mAdapter;
    private SharedPreferences prefs;
    public  static final String[] AD_CATS = new String[]{"Cars", "Clothes", "Food", "Tech", "Video Games", "Vacations"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ad_prefs);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        prefs = getSharedPreferences("personal", MODE_PRIVATE);
        getAdPrefs();
        ListView listView = findViewById(R.id.ad_prefs_list);
        mAdapter = new AdPrefsAdapter(this, ad_map);
        listView.setAdapter(mAdapter);

    }


    public void SetupWalletClick2(View view) {
        Log.i("AdPrefs", "Saving Add Prefs in SharedPrefs");
        saveAdPrefs();
        Intent intent = new Intent(this, SetupWalletActivity.class);
        startActivity(intent);
    }

    private void saveAdPrefs(){
        SharedPreferences.Editor editor = prefs.edit();
        for(int i = 0; i < mAdapter.getCount(); i++){
            editor.putFloat(mAdapter.getKey(i), mAdapter.getItem(i));
        }
        editor.apply();
    }

    private void getAdPrefs(){
        for (String AD_CAT : AD_CATS) {
            ad_map.put(AD_CAT, prefs.getFloat(AD_CAT, 5f));
        }
    }

}
