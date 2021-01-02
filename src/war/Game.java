package war;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Game {
    int turn;
    public static ArrayList<Row> moves = new ArrayList<Row>();
    Player[] players;

    public Game(int numPlayers) {
        players = new Player[numPlayers];
        turn = 0;
        parseMoves("src/war/moves/moves.txt");
        for(int i = 0; i < numPlayers; i++) {
            players[i] = new Player("Player" + (i + 1)); // placeholder name;
        }
    }


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
}
