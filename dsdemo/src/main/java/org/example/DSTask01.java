package org.example;

import cn.hutool.core.util.StrUtil;

import java.util.ArrayList;
import java.util.List;
//import java.util.stream.IntStream;

public class DSTask01 {
    public static void main(String[] args) {
        long beforeUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long beforeTime = System.currentTimeMillis();
        execute(Integer.parseInt(args[0]));
        long afterUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        double actualMemUsed = (afterUsedMem - beforeUsedMem) * 1.0 / (1024 * 1024);
        long afterTime = System.currentTimeMillis();
        double actualTimeUsed = (afterTime - beforeTime) * 1.0 / 1000;
        System.out.println(StrUtil.format("Space costs:{}MB,Time costs:{}s", actualMemUsed, actualTimeUsed));
    }

    private static void execute(int max) {
        List<Integer> odd = new ArrayList<>();
        List<Integer> even = new ArrayList<>();

        for (int i = 0; i < max; i++) {
            if (i % 2 == 0) {
                odd.add(i);
            } else {
                even.add(i);
            }
        }

        System.out.println("ODD numbers:" + odd);
        System.out.println("EVEN numbers:" + even);
//        IntStream.range(1,max).filter(x->x%2==0).forEach(System.out::println);
//        IntStream.range(1,max).filter(x->x%2==1).forEach(System.out::println);
    }
}