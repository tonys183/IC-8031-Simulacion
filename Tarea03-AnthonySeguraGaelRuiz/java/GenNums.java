import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public class GenNums {
    public static void main(String[] args) {
        int n = 1000000;
        try (FileWriter fw = new FileWriter("java.txt");
             BufferedWriter bw = new BufferedWriter(fw);
             PrintWriter out = new PrintWriter(bw)) {

            Random random = new Random();
            for (int i=0; i<n; i++) out.println(random.nextDouble());
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}