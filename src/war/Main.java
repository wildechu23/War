package war;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        boolean running = true;

        Game game = new Game(2);

        for(int i = 0; i < 2; i++) {
            game.round();
        }

//        while(running) {
//
//        }
    }

}
