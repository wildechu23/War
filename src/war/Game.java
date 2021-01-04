package war;

import war.moves.Attack;
import war.moves.Defense;
import war.moves.Move;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Game {
    int turn;
    public static ArrayList<Row> moves = new ArrayList<>();
    private static ArrayList<Player> players;

    public Game(int numPlayers) {
        players = new ArrayList<>();
        turn = 0;
        parseMoves("src/war/moves/moves.txt");
        for(int i = 0; i < numPlayers; i++) {
            players.add(new Player("Player" + (i + 1))); // placeholder name;
        }
    }

    public void round() {
        for (Player player : players) {
            if(player.isAlive()) {
                player.turn();
                System.out.println(player.getName());
                System.out.println("Attack: " + player.attack);
                System.out.println("Defense: " + player.defense);
                System.out.println(player.listResources());
            } else {
                players.remove(player);
            }
        }
        // TODO: FIGHT FIGHT FIGHT FIGHT
        fight();
    }

    public void fight() {
        // each interaction once
        for(int i = 0; i < players.size(); i++) {
            Player player1 = players.get(i);
            for(int j = i + 1; j < players.size(); j++) {
                int attack1 = 0, attack2 = 0, defense1 = 0, defense2 = 0;
                Player player2 = players.get(j);
                System.out.println("Player 1: " + player1.getName());
                System.out.println("Player 2: " + player2.getName());

                // Player 1 strength
                for(Move move : player1.getMoves()) {
                    System.out.println(move);
                    if(move instanceof Attack) {
                        if (player2.getName() == ((Attack) move).getTarget().getName()) {
                            attack1 += ((Attack) move).damageOf();
                        }
                    }
                    if(move instanceof Defense) {
                        defense1 += ((Defense) move).strengthOf();
                    }
                }

                //Player 2 strength
                for(Move move : player2.getMoves()) {
                    System.out.println(move);
                    if(move instanceof Attack) {
                        if (player1.getName() == ((Attack) move).getTarget().getName()) {
                            attack2 += ((Attack) move).damageOf();
                        }
                    }
                    if(move instanceof Defense) {
                        defense2 += ((Defense) move).strengthOf();
                    }
                }

                System.out.println("Attack1: " + attack1 + ", Defense1: " + defense1);
                System.out.println("Attack2: " + attack2 + ", Defense2: " + defense2);

                if(attack1 > attack2 + defense2) {
                    player2.kill(); // if player 1 attack is greater than player 2 strength, kill player 2
                    System.out.println(player2.getName() + " was killed by " + player1.getName());
                } else if (attack2 > attack1 + defense1) {
                    player1.kill(); // if player 2 attack is greater than player 1 strength, kill player 1
                    System.out.println(player1.getName() + " was killed by " + player2.getName());
                } else {
                    //leave alone;
                }
            }
        }
    }

    // is this needed?
    public static void parseMoves(String file) {
        File f = new File(file);
        try {
            Scanner s = new Scanner(f);
            while (s.hasNextLine()) {
                String line = s.nextLine();
                String[] tokens = line.split(", ");
                Row row = new Row(tokens[0], Integer.parseInt(tokens[1]), tokens[2], Integer.parseInt(tokens[3]),
                        Integer.parseInt(tokens[4]), Integer.parseInt(tokens[5]), Integer.parseInt(tokens[6]),
                        Integer.parseInt(tokens[7]), Integer.parseInt(tokens[8]));
                moves.add(row);
            }
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    // moves table row class
    public static class Row {
        private String type, costType;
        private int cost, attack, defense, charges, blocks, doubles, smokes;

        public Row(String type, int cost, String costType, int attack, int defense,
                   int charges, int blocks, int doubles, int smokes) {
            this.type = type;
            this.cost = cost;
            this.costType = costType;
            this.attack = attack;
            this.defense = defense;
            this.charges = charges;
            this.blocks = blocks;
            this.doubles = doubles;
            this.smokes = smokes;
        }

        public String getType() { return type; }
        public int getCost() { return cost; }
        public String getCostType() { return costType; }

        public int getAttack() { return attack; }
        public int getDefense() { return defense; }
        public int getCharges() { return charges; }
        public int getBlocks() { return blocks; }
        public int getDoubles() { return doubles; }
        public int getSmokes() { return smokes; }
    }

    public static ArrayList<Player> getPlayers() {
        return players;
    }
}
