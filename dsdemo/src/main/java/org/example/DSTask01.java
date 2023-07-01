package org.example;

import cn.hutool.core.util.StrUtil;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DSTask01 {
    private static final String PDF = "./pdf.pdf";
    
    public static void main(String[] args) {
        long beforeUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long beforeTime = System.currentTimeMillis();
        execute();
        long afterUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        double actualMemUsed = (afterUsedMem - beforeUsedMem) * 1.0 / (1024 * 1024);
        long afterTime = System.currentTimeMillis();
        double actualTimeUsed = (afterTime - beforeTime) * 1.0 / 1000;
        System.out.println(StrUtil.format("Space costs:{}MB,Time costs:{}s", actualMemUsed, actualTimeUsed));
    }

    private static void execute() {
        try {
            File file = new File(PDF);

            RequestBody requestBody = new MultipartBody.Builder().setType(MultipartBody.FORM)
                    .addFormDataPart("file", file.getName(),RequestBody.create(MediaType.parse("application/octet-stream"), file))
                    .build();

            Request request = new Request.Builder()
                    .url("https://file.moringstars.com/upload")
                    .post(requestBody)
                    .build();

            OkHttpClient client = new OkHttpClient();
            try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) 
                throw new IOException("Unexpected code " + response);
                System.out.println(response.body().string());
            }
        } catch (FileNotFoundException | DocumentException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}