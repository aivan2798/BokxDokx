package com.blakbokx.bokxdocs.workers;

import android.content.Context;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import android.util.Log;
import com.blakbokx.bokxdocs.ui.home.PdfViewFragment;
import com.tom_roush.pdfbox.pdmodel.PDDocument;
import com.tom_roush.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

public class PdfBokx {
    public PDDocument pdf_doc;
    public String pdf_text;
    public PdfBokx(Context context, Uri file_uri){
        try{
            InputStream is = context.getContentResolver().openInputStream(file_uri);

            PDFTextStripper stripper = new PDFTextStripper();




            pdf_doc = PDDocument.load(is);
            //String text = stripper.getText(pdf_doc);
            pdf_text = stripper.getText(pdf_doc);
            pdf_doc.close();
            is.close();
        } catch (IOException e) {
            Log.e("[PDFBokx]",e.getMessage());
        }
    }
}
