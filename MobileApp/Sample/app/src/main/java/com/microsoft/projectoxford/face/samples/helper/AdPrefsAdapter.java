package com.microsoft.projectoxford.face.samples.helper;

import com.microsoft.projectoxford.face.samples.R;
import android.content.Context;
import android.media.Rating;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.RatingBar;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Set;

public class AdPrefsAdapter extends ArrayAdapter<Float> {
    private final Context context;
    private HashMap<String, Float> ratingMap;
    private final String[] values;

    public AdPrefsAdapter(@NonNull Context context, @NonNull HashMap<String, Float> objects) {
        super(context, R.layout.ad_pref);
        ratingMap = new HashMap<>();
        values = new String[objects.keySet().size()];
        objects.keySet().toArray(values);
        ratingMap = objects;
        this.context = context;
    }

    @Override
    public int getCount() {
        return values.length;
    }

    public String getKey(int pos){
        return values[pos];
    }

    @NonNull
    @Override
    public Float getItem(int position) {
        return ratingMap.get(values[position]);
    }


   @Override
    public View getView(int position, View convertView, ViewGroup container) {
        final int P = position;
        if (convertView == null) {
            LayoutInflater inflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            assert inflater != null;
            convertView = inflater.inflate(R.layout.ad_pref, container, false);
        }

        ((TextView) convertView.findViewById(R.id.ad_pref_text))
                .setText(getKey(position));

        RatingBar ratingBar = (RatingBar) convertView.findViewById(R.id.ratingBar);
        ratingBar.setRating(getItem(position));
        final RatingBar.OnRatingBarChangeListener ratingListener = new RatingBar.OnRatingBarChangeListener() {
           @Override
           public void onRatingChanged(RatingBar ratingBar, float rating, boolean fromUser) {
               ratingMap.put(values[P], rating);
            }
       };

        ratingBar.setOnRatingBarChangeListener(ratingListener);

        return convertView;
    }
}
