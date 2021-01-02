package war;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner keyboard = new Scanner(System.in);
        boolean running = true;

        Game game = new Game(2);

        for(Player player : game.players) {
            player.turn();
            System.out.println(player.getName());
            System.out.println("Attack: " + player.attack);
            System.out.println("Defense: " + player.defense);
            System.out.println("Blocks: " + player.blocks());
        }

//        while(running) {
//
//        }
    }

}
