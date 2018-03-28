package com.microsoft.projectoxford.face.samples.ui;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;

import com.microsoft.projectoxford.face.FaceServiceClient;
import com.microsoft.projectoxford.face.contract.CreatePersonResult;
import com.microsoft.projectoxford.face.samples.R;
import com.microsoft.projectoxford.face.samples.helper.FaceClientApp;
import com.microsoft.projectoxford.face.samples.persongroupmanagement.PersonActivity;

public class UserDetailsActivity extends AppCompatActivity {
    private String imgUri;
    private String personId;
    private UserDetailsActivity self;
    private ProgressBar progressBar;
    private SharedPreferences prefs;
    private String name;
    private String pin;
    private String faceGroup;
    private EditText nameEditText;
    private EditText pinEditText;
    private Button nextButton;
    private boolean addedFaces;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_details);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        // Get a support ActionBar corresponding to this toolbar
        ActionBar ab = getSupportActionBar();
        // Enable the Up button
        assert ab != null;
        ab.setDisplayHomeAsUpEnabled(true);

        faceGroup = "large-person-group-1";
        self = this;
        progressBar = (ProgressBar) findViewById(R.id.createPersonLoader);
        nameEditText = (EditText) findViewById(R.id.nameEditText);
        pinEditText = (EditText) findViewById(R.id.pinEditText);
        nextButton = (Button) findViewById(R.id.createPersonButton2);
        progressBar.setVisibility(View.INVISIBLE);
        nextButton.setEnabled(true);

        prefs = getSharedPreferences("personal", MODE_PRIVATE);
        personId = prefs.getString("PersonId", null);
        if (personId != null) {
            name = prefs.getString("PersonName", "No name defined");//"No name defined" is the default value.
            pin = prefs.getString("pin", "XXXX"); //0 is the default value.
            nameEditText.setText(name);
            pinEditText.setText(pin);
        }

        //TODO DEBUG ONLY
        this.getSharedPreferences("personal", MODE_PRIVATE).edit().clear().apply();
        personId = null;
        //END DEBUG ONLY

    }

    @Override
    public void onResume() {
        super.onResume();  // Always call the superclass method first

        if(addedFaces){
            Button setupWallet = (Button) findViewById(R.id.setupWallet);
            setupWallet.setEnabled(true);
        }
    }

    /**
     * Click event that creates a person in Large-Person-Group-1 with a name and pin
     */
    public void CreatePersonClick(View view) {
        String nameText = nameEditText.getText().toString();
        String pinText = pinEditText.getText().toString();

        if(!pinText.equals("") && !nameText.equals("")) {
            if (personId == null) {
                progressBar.setVisibility(View.VISIBLE);
                nextButton.setEnabled(false);
                new AddPersonTask(true, nameText, pinText).execute(faceGroup);
            } else {
                //TODO if personId is already created, then just add faces
                Snackbar snackbar = Snackbar.make(view, "Account already created", Snackbar.LENGTH_LONG);
                snackbar.show();
            }
        }
        else{
            Snackbar snackbar = Snackbar.make(view, "Missing Information", Snackbar.LENGTH_LONG);
            snackbar.show();
        }
    }

    public void SetupWalletClick(View view) {
        Intent intent = new Intent(this, SetupWallet.class);
        intent.putExtra("PersonId", personId);
        intent.putExtra("PersonName", name);
        intent.putExtra("personPin", pin);
        intent.putExtra("PersonGroupId", faceGroup);
        startActivity(intent);
    }

    // Background task of adding a person to large-person group.
    @SuppressLint("StaticFieldLeak")
    class AddPersonTask extends AsyncTask<String, String, String> {
        // Indicate the next step is to add face in this person, or finish editing this person.
        boolean mAddFace;

        AddPersonTask (boolean addFace, String n, String p) {
            mAddFace = addFace;
            name  = n;
            pin = p;
        }

        @Override
        protected String doInBackground(String... params) {
            // Get an instance of face service client.
            FaceServiceClient faceServiceClient = FaceClientApp.getFaceServiceClient();
            try{
                publishProgress("Syncing with server to add person...");
                Log.i("FaceClient","Request: Creating Person in person group" + params[0]);

                // Start the request to creating person.
                CreatePersonResult createPersonResult = faceServiceClient.createPersonInLargePersonGroup(
                        params[0], name,"");
                //getString(R.string.user_provided_person_name),

                return createPersonResult.personId.toString();
            } catch (Exception e) {
                publishProgress(e.getMessage());
                Log.i("FaceClient",e.getMessage());
                nextButton.setEnabled(true);
                return null;
            }
        }

        @Override
        protected void onPreExecute() {
            //setUiBeforeBackgroundTask();
            Log.i("Starting", "Starting  person creation");
        }

        @Override
        protected void onProgressUpdate(String... progress) {
            //setUiDuringBackgroundTask(progress[0]);
            Log.i("Working", progress[0]);
        }

        @Override
        protected void onPostExecute(String result) {
            Log.i("Done", "done");
            if (result != null) {
                Log.i("Faceclient", "Response: Success. Person " + result + " created.");
                personId = result;

                progressBar.setVisibility(View.INVISIBLE);

                SharedPreferences.Editor editor = prefs.edit();
                editor.putString("PersonId", personId);
                editor.putString("name", name);
                editor.putString("pin", pin);
                editor.apply();
                nextButton.setEnabled(true);
                Intent intent = new Intent(self, PersonActivity.class);
                intent.putExtra("PersonId", personId);
                intent.putExtra("PersonName", name);
                intent.putExtra("personPin", pin);
                intent.putExtra("PersonGroupId", faceGroup);
                startActivity(intent);

                //TODO not good error checking...
                addedFaces = true;

            }
        }
    }

}
