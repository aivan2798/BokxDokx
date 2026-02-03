package com.blakbokx.bokxdocs.ui.home;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentContainer;
import androidx.fragment.app.FragmentContainerView;
import androidx.fragment.app.FragmentManager;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.blakbokx.bokxdocs.DataPack.FilePack;
import com.blakbokx.bokxdocs.R;
import com.blakbokx.bokxdocs.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {

    private static final int FILE_PICK_REQUEST = 1001;
    private static final int PERMISSION_REQUEST_CODE = 200;
    private FragmentHomeBinding binding;
    private HomeViewModel homeViewModel;
    private  View pdf_view_fragment;
    private FragmentManager parent_fragment_manager;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        parent_fragment_manager  = getParentFragmentManager();
        final TextView textView = binding.textHome;
        final ImageButton add_file_btn = binding.addFileBtn;
        final LinearLayout add_file_parent = binding.noFileLayout;
        final FragmentContainerView pdf_fragment_container = binding.pdfContainer;
        add_file_btn.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        checkPermissionAndPick(v);
                    }
                }
        );
        homeViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
        homeViewModel.getLoadStatus().observe(getViewLifecycleOwner(), new Observer<Boolean>() {
            @Override
            public void onChanged(Boolean aBoolean) {
                if(aBoolean==true){
                    //pdf_view_fragment = getLayoutInflater().inflate(R.layout.fragment_pdf_view,null);

                    //textView.setText("File loaded: "+FilePack.active_file_uri.toString());
                    add_file_parent.removeAllViews();

                    //add_file_parent.addView(pdf_view_fragment);
                    parent_fragment_manager.beginTransaction().replace(R.id.pdf_container,new PdfViewFragment(FilePack.active_file_uri)).commit();
                }
                else{
                    textView.setText("No File Present");
                }
            }
        });
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    public void openFileChooser() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("*/*"); // all file types

        // optional — only show openable files
        intent.addCategory(Intent.CATEGORY_OPENABLE);

        startActivityForResult(intent, FILE_PICK_REQUEST);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == FILE_PICK_REQUEST && resultCode == Activity.RESULT_OK && data != null) {
            Uri fileUri = data.getData();

            if (fileUri != null) {

                FilePack.active_file_uri = fileUri;
                Toast.makeText(this.getContext(), "Selected: " + fileUri.toString(), Toast.LENGTH_LONG).show();
                homeViewModel.setLoadStatus(true);
                // You can now open input stream:
                // InputStream is = getContentResolver().openInputStream(fileUri);
            }
        }
    }

    public void checkPermissionAndPick(View vw) {
        if (ContextCompat.checkSelfPermission(this.getContext(),
                Manifest.permission.READ_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(
                    this.getActivity(),
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                    PERMISSION_REQUEST_CODE
            );

        } else {
            openFileChooser();
        }
    }
}