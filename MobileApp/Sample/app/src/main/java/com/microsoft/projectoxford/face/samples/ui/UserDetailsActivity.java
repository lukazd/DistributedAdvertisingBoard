package com.microsoft.projectoxford.face.samples.ui;

import android.annotation.SuppressLint;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
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
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import com.microsoft.projectoxford.face.FaceServiceClient;
import com.microsoft.projectoxford.face.contract.CreatePersonResult;
import com.microsoft.projectoxford.face.samples.R;
import com.microsoft.projectoxford.face.samples.helper.FaceClientApp;
import com.microsoft.projectoxford.face.samples.persongroupmanagement.PersonActivity;

import java.util.Calendar;

public class UserDetailsActivity extends AppCompatActivity {
    private String imgUri;
    private String personId;
    private UserDetailsActivity self;
    private ProgressBar progressBar;
    private SharedPreferences prefs;
    private String name;
    private static String bday;
    private String sex;
    private String faceGroup;
    private EditText nameEditText;
    private EditText pinEditText;
    private Button nextButton;
    private boolean addedFaces;
    @SuppressLint("StaticFieldLeak")
    private static TextView birthEdit;
    private boolean editMode;
    private Button setupWallet;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_details);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        // Get a support ActionBar corresponding to this toolbar


        faceGroup = "large-person-group-1"; //TODO hardcoded group for now.
        self = this;
        progressBar = findViewById(R.id.createPersonLoader);
        nameEditText = findViewById(R.id.nameEditText);
        nextButton = findViewById(R.id.createPersonButton2);
        birthEdit = findViewById(R.id.birthEdit);
        progressBar.setVisibility(View.INVISIBLE);
        nextButton.setEnabled(true);

        setupWallet = findViewById(R.id.setupWallet);

        prefs = getSharedPreferences("personal", MODE_PRIVATE);
        personId = prefs.getString("PersonId", null);
        editMode = false;
        if (personId != null) {
            editMode = true;
            setupWallet.setEnabled(true);

            name = prefs.getString("name", "No name defined");//"No name defined" is the default value.
            sex = prefs.getString("sex", "male");
            bday = prefs.getString("bday", "Not defined");
            birthEdit.setText(bday);
            nameEditText.setText(name);
        }

        //DEBUG ONLY
        //this.getSharedPreferences("personal", MODE_PRIVATE).edit().clear().apply();
        //personId = null;
        //END DEBUG ONLY

    }

    @Override
    public void onResume() {
        super.onResume();  // Always call the superclass method first
        if(addedFaces){
            setupWallet.setEnabled(true);
        }
    }

    /**
     * Click event that creates a person in Large-Person-Group-1 with a name and pin
     */
    public void CreatePersonClick(View view) {
        String nameText = nameEditText.getText().toString();
        bday =  birthEdit.getText().toString();
        RadioGroup radioSexGroup = findViewById(R.id.radioSex);
        // get selected radio button from radioGroup
        int selectedId = radioSexGroup.getCheckedRadioButtonId();
        // find the radiobutton by returned id
        RadioButton radioSexButton = findViewById(selectedId);

        if( !nameText.equals("") && !bday.equals("")) {
            if (personId == null) {
                progressBar.setVisibility(View.VISIBLE);
                nextButton.setEnabled(false);
                new AddPersonTask(true, nameText, bday, radioSexButton.getText().toString()).execute(faceGroup);
            } else {
                Snackbar snackbar = Snackbar.make(view, "Account already created", Snackbar.LENGTH_LONG);
                snackbar.show();
                Intent intent = new Intent(self, PersonActivity.class);
                intent.putExtra("PersonId", personId);
                intent.putExtra("PersonName", name);
                intent.putExtra("PersonGroupId", faceGroup);
                startActivity(intent);
            }
        }
        else{
            Snackbar snackbar = Snackbar.make(view, "Missing Information", Snackbar.LENGTH_LONG);
            snackbar.show();
        }
    }

    public void SetupWalletClick(View view) {
        Intent intent = new Intent(this, AdPrefsActivity.class);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString("PersonId", personId);
        editor.putString("name", name);
        editor.putString("bday", bday);
        editor.putString("sex", sex);
        editor.putString("personGroupId", faceGroup);
        editor.apply();
        startActivity(intent);
    }

    public void showDatePickerDialog(View view) {
        DialogFragment newFragment = new DatePickerFragment();
        newFragment.show(getFragmentManager(), "datePicker");
    }

    // Background task of adding a person to large-person group.
    @SuppressLint("StaticFieldLeak")
    class AddPersonTask extends AsyncTask<String, String, String> {
        // Indicate the next step is to add face in this person, or finish editing this person.
        boolean mAddFace;

        AddPersonTask (boolean addFace, String n, String bd, String sx) {
            mAddFace = addFace;
            name  = n;
            bday = bd;
            sex = sx;
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
                editor.putString("bday", bday);
                editor.putString("sex", sex);
                editor.putString("personGroupId", faceGroup);
                editor.apply();
                nextButton.setEnabled(true);
                Intent intent = new Intent(self, PersonActivity.class);
                intent.putExtra("PersonId", personId);
                intent.putExtra("PersonName", name);
                intent.putExtra("PersonGroupId", faceGroup);
                startActivity(intent);
                addedFaces = true;
            }
        }
    }

    public static class DatePickerFragment extends DialogFragment implements DatePickerDialog.OnDateSetListener {
        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            // Use the current date as the default date in the picker
            final Calendar c = Calendar.getInstance();
            int year = c.get(Calendar.YEAR);
            int month = c.get(Calendar.MONTH) + 1;
            int day = c.get(Calendar.DAY_OF_MONTH);

            // Create a new instance of DatePickerDialog and return it
            return new DatePickerDialog(getActivity(), this, year, month, day);
        }

        public void onDateSet(DatePicker view, int year, int month, int day) {
            // Do something with the date chosen by the user
            String sb = String.valueOf(month + 1) + "/" + day + "/" + year;
            assert birthEdit != null;
            birthEdit.setText(sb);
            bday = sb;
        }
    }


}
