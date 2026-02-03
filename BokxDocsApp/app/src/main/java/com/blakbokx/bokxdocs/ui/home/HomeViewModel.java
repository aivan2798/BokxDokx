package com.blakbokx.bokxdocs.ui.home;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class HomeViewModel extends ViewModel {

    private final MutableLiveData<String> mText;
    private final MutableLiveData<Boolean> file_loaded;

    public HomeViewModel() {
        mText = new MutableLiveData<>();
        file_loaded =  new MutableLiveData<>();
        file_loaded.setValue(false);
        mText.setValue("No File Present");
    }

    public LiveData<Boolean> getLoadStatus(){
        return file_loaded;
    }

    public void setLoadStatus(Boolean load_status){
        file_loaded.setValue(load_status);
    }
    public LiveData<String> getText() {
        return mText;
    }
}