package com.blakbokx.bokxdocs.ui.home;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.MainThread;
import androidx.fragment.app.Fragment;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.blakbokx.bokxdocs.R;
import com.blakbokx.bokxdocs.workers.PdfBokx;

public class PdfViewFragment extends Fragment {


    private Uri active_pdf_file;
    private PdfBokx pdf_bokx;
    public PdfViewFragment(Uri pdf_uri){
        active_pdf_file = pdf_uri;
    }

    Thread pdf_loader;
    private Activity active_activity;
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View pdf_view = inflater.inflate(R.layout.fragment_pdf_view, container, false);
        active_activity = getActivity();
        pdf_loader = new Thread(new Runnable() {
            @Override
            public void run() {
                Log.i("[PDF_LOADER]","started loading");
                pdf_bokx = new PdfBokx(getContext(),active_pdf_file);
                Log.i("[PDF_LOADER]","finished loading");
                active_activity.runOnUiThread(
                        new Runnable() {
                            @Override
                            public void run() {
                                ((TextView)pdf_view.findViewById(R.id.text_pdf)).setText(pdf_bokx.pdf_text);
                            }
                        }
                );

            }
        });

        pdf_loader.start();


        ((TextView)pdf_view.findViewById(R.id.text_pdf)).setText("Loading PDF, please wait");

        return pdf_view;
    }
}