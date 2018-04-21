package com.microsoft.projectoxford.face.samples.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.SparseArray;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.vision.Frame;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;

import com.google.firebase.FirebaseApp;
import com.google.firebase.firestore.FirebaseFirestore;
import com.microsoft.projectoxford.face.samples.BuildConfig;
import com.microsoft.projectoxford.face.samples.R;
import com.microsoft.projectoxford.face.samples.helper.SenseAdInfoModel;

import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

import static com.microsoft.projectoxford.face.samples.ui.AdPrefsActivity.AD_CATS;

public class SetupWalletActivity extends AppCompatActivity {


    private SharedPreferences prefs;

    private static final String LOG_TAG = "Barcode Scanner API";
    private static final int PHOTO_REQUEST = 10;
    private TextView scanResults;
    private BarcodeDetector detector;
    private Uri imageUri;
    private static final String SAVED_INSTANCE_URI = "uri";
    private static final String SAVED_INSTANCE_RESULT = "result";
    private static final int REQUEST_IMAGE_CAPTURE = 2;
    private String mCurrentPhotoPath;
    private EditText iotaEditText;
    private String iotaCode;
    private SenseAdInfoModel senseAdInfo;
    private Map<String, Float> ad_map;

    private boolean isEdit;


    private FirebaseFirestore firestoreDB;
    private SetupWalletActivity self;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup_wallet);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        FirebaseApp.initializeApp(this);
        self = this;

        Bundle bundle = getIntent().getExtras();
        String personName;
        String personId;
        String personGroupId;

        prefs = getSharedPreferences("personal", MODE_PRIVATE);
        personId = prefs.getString("PersonId", null);

        personName = prefs.getString("name", "No name defined");//"No name defined" is the default value.
        String sex = prefs.getString("sex", "male");
        String bday = prefs.getString("bday", "Not defined");
        String faceGroupName = prefs.getString("personGroupId", "large-person-group-1");
        iotaCode = prefs.getString("iotaCode", null);
        ad_map = new HashMap<>();
        getAdPrefs();
        senseAdInfo = new SenseAdInfoModel(sex, bday, faceGroupName, personName, personId, ad_map);

        isEdit = iotaCode != null;

        Button browseButton = (Button) findViewById(R.id.button);
        scanResults = (TextView) findViewById(R.id.txtContent);
        if (savedInstanceState != null) {
            imageUri = Uri.parse(savedInstanceState.getString(SAVED_INSTANCE_URI));
            scanResults.setText(savedInstanceState.getString(SAVED_INSTANCE_RESULT));
        }
        browseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                browsePhoto();
            }
        });

        Button captureButton = (Button) findViewById(R.id.captureButton);
        captureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dispatchTakePictureIntent();
            }
        });

        iotaEditText = (EditText) findViewById(R.id.wallet_address_edit);

        if(iotaCode != null){
            iotaEditText.setText(iotaCode);
        }


        detector = new BarcodeDetector.Builder(getApplicationContext())
                .setBarcodeFormats(Barcode.DATA_MATRIX | Barcode.QR_CODE)
                .build();
        if (!detector.isOperational()) {
            scanResults.setText(R.string.cant_setup);
        }


        firestoreDB = FirebaseFirestore.getInstance();
    }

    private void getAdPrefs(){
        for (String AD_CAT : AD_CATS) {
            ad_map.put(AD_CAT, prefs.getFloat(AD_CAT, 5f));
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == PHOTO_REQUEST && resultCode == RESULT_OK) {
            imageUri = data.getData();
            scanBarCode();
        }

        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            imageUri = Uri.parse(mCurrentPhotoPath);
            scanBarCode();
        }
    }

    /**
     * Code handling taking a picture
     */
    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        // Ensure that there's a camera activity to handle the intent
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            // Create the File where the photo should go
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                // Error occurred while creating the File
            }
            // Continue only if the File was successfully created
            if (photoFile != null) {
                Uri photoURI = null;
                try {
                    photoURI = FileProvider.getUriForFile(SetupWalletActivity.this,
                            BuildConfig.APPLICATION_ID + ".provider",
                            createImageFile());
                } catch (IOException e) {
                    e.printStackTrace();
                }
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                takePictureIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
            }
        }
    }

    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DCIM), "Camera");
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        mCurrentPhotoPath = "file:" + image.getAbsolutePath();
        return image;
    }

    public void scanBarCode(){
        launchMediaScanIntent();
        try {
            Bitmap bitmap = decodeBitmapUri(this, imageUri);
            if (detector.isOperational() && bitmap != null) {
                Frame frame = new Frame.Builder().setBitmap(bitmap).build();
                SparseArray<Barcode> barcodes = detector.detect(frame);
                for (int index = 0; index < barcodes.size(); index++) {
                    Barcode code = barcodes.valueAt(index);
                    scanResults.setText(R.string.IOTA_Code);
                    try {
                        JSONObject jsonObject = new JSONObject(code.displayValue);
                        String s = (String) jsonObject.get("address");
                        iotaEditText.setText(s);
                        senseAdInfo.setIotaCode(s);
                    } catch (Throwable throwable){
                        Log.e("QR Reader", "Could not pase malformed JSON");
                        scanResults.setText(R.string.try_again);
                    }

                    //Required only if you need to extract the type of barcode
                    int type = barcodes.valueAt(index).valueFormat;
                    switch (type) {
                        case Barcode.CONTACT_INFO:
                            Log.i(LOG_TAG, code.contactInfo.title);
                            break;
                        case Barcode.EMAIL:
                            Log.i(LOG_TAG, code.email.address);
                            break;
                        case Barcode.ISBN:
                            Log.i(LOG_TAG, code.rawValue);
                            break;
                        case Barcode.PHONE:
                            Log.i(LOG_TAG, code.phone.number);
                            break;
                        case Barcode.PRODUCT:
                            Log.i(LOG_TAG, code.rawValue);
                            break;
                        case Barcode.SMS:
                            Log.i(LOG_TAG, code.sms.message);
                            break;
                        case Barcode.TEXT:
                            Log.i(LOG_TAG, code.rawValue);
                            break;
                        case Barcode.URL:
                            Log.i(LOG_TAG, "url: " + code.url.url);
                            break;
                        case Barcode.WIFI:
                            Log.i(LOG_TAG, code.wifi.ssid);
                            break;
                        case Barcode.GEO:
                            Log.i(LOG_TAG, code.geoPoint.lat + ":" + code.geoPoint.lng);
                            break;
                        case Barcode.CALENDAR_EVENT:
                            Log.i(LOG_TAG, code.calendarEvent.description);
                            break;
                        case Barcode.DRIVER_LICENSE:
                            Log.i(LOG_TAG, code.driverLicense.licenseNumber);
                            break;
                        default:
                            Log.i(LOG_TAG, code.rawValue);
                            break;
                    }
                }
                if (barcodes.size() == 0) {
                    scanResults.setText(R.string.Scan_failed);
                }
            } else {
                scanResults.setText(R.string.no_detector);
            }
        } catch (Exception e) {
            Toast.makeText(this, "Failed to load Image", Toast.LENGTH_SHORT)
                    .show();
            Log.e(LOG_TAG, e.toString());
        }
    }

    private void browsePhoto() {
        Intent gallIntent = new Intent(Intent.ACTION_GET_CONTENT);
        gallIntent.setType("image/*");
        startActivityForResult(Intent.createChooser(gallIntent, "Select Picture"), PHOTO_REQUEST);
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        if (imageUri != null) {
            outState.putString(SAVED_INSTANCE_URI, imageUri.toString());
            outState.putString(SAVED_INSTANCE_RESULT, scanResults.getText().toString());
        }
        super.onSaveInstanceState(outState);
    }

    private void launchMediaScanIntent() {
        Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        mediaScanIntent.setData(imageUri);
        this.sendBroadcast(mediaScanIntent);
    }

    private Bitmap decodeBitmapUri(Context ctx, Uri uri) throws FileNotFoundException {
        int targetW = 600;
        int targetH = 600;
        BitmapFactory.Options bmOptions = new BitmapFactory.Options();
        bmOptions.inJustDecodeBounds = true;
        BitmapFactory.decodeStream(ctx.getContentResolver().openInputStream(uri), null, bmOptions);
        int photoW = bmOptions.outWidth;
        int photoH = bmOptions.outHeight;

        int scaleFactor = Math.min(photoW / targetW, photoH / targetH);
        bmOptions.inJustDecodeBounds = false;
        bmOptions.inSampleSize = scaleFactor;

        return BitmapFactory.decodeStream(ctx.getContentResolver()
                .openInputStream(uri), null, bmOptions);
    }

    public void SaveToFireBase(View view) {
        senseAdInfo.setIotaCode(iotaEditText.getText().toString());
        iotaCode = senseAdInfo.getIotaCode();
        if(iotaCode == null || senseAdInfo.getIotaCode().length() != 90){
            Snackbar.make(view, "IOTA Address Incorrect", Snackbar.LENGTH_LONG).show();
            return;
        }
        SharedPreferences.Editor editor =  prefs.edit();
        editor.putString("iotaCode", iotaCode);
        editor.apply();

        addDocumentToCollection(senseAdInfo);

    }

    private void addDocumentToCollection(SenseAdInfoModel personInfo){
          firestoreDB.collection("personInfo")
                .document(personInfo.getPersonId())
                .set(personInfo)
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void aVoid) {
                        Log.d("Firestore", "DocumentSnapshot successfully written!");
                        Intent intent = new Intent(self, LoggedInActivity.class);
                        startActivity(intent);
                    }
                })
                .addOnFailureListener(new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        Log.w("Firestore", "Error adding event document", e);
                        Snackbar.make(self.findViewById(R.id.ratingBar), "Problems Saving Information, Try again.", Snackbar.LENGTH_LONG).show();
                    }
                });
    }
}
