package war;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        boolean running = true;

        Game game = new Game(2);

        while(Game.getPlayers().size() > 1) {
            game.round();
        }
//        while(running) {
//
//        }
    }

}
