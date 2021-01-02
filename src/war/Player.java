package war;

import war.moves.*;

import java.util.ArrayList;
import java.util.Scanner;

public class Player {
    private String name;
    private int chargeCount, blockCount, doubleCount, smokeCount;
    private Move move;
    private Player target;
    private boolean alive;
    private boolean havePewCharge;

    public int attack = 0, defense = 0;

    public Player(String name) {
        this.name = name;
        chargeCount = 0;
        blockCount = 0;
        alive = true;
        havePewCharge = true;
    }

    public void turn() {
        resetStats();
        ArrayList<Move> moves = inputMove();

        for(Move thisMove : moves) {
            // if it gives resources
            if (thisMove instanceof Resource) {
                // each resource in the list of resources
                for (Resource.Resources r : ((Resource) thisMove).resources()) {
                    switch (r) {
                        case CHARGE:
                            addCharge();
                            break;
                        case BLOCK:
                            addBlock();
                            break;
                        case DOUBLE:
                            addDouble();
                            break;
                        case SMOKE:
                            addSmoke();
                            break;
                        default:
                            throw new IllegalArgumentException("Shouldn't be possible to get here, " +
                                    "but thisMove.resources() has a resource not one of these types");
                    }
                }
            }

            // TODO: check if has valid number of resources
            if (thisMove instanceof Attack) {
                attack += ((Attack) thisMove).damageOf();
            } else if (thisMove instanceof Defense) {
                defense += ((Defense) thisMove).strengthOf();
            }
        }
    }

    // input from console
    public ArrayList<Move> inputMove() {
        Scanner s = new Scanner(System.in);
        System.out.println("Enter Moves");
        String input = s.nextLine();
        String[] inputList = input.split(" "); // split by spaces
        // if inputMove is Attack, ask target
        ArrayList<Move> moves = new ArrayList<Move>();
        for(String i : inputList) {
            moves.add(parseInput(i));
        }
        return moves;
    }

    public Move parseInput(String string) {
        switch(string) {
            // Pew
            case "p":
            case "P":
                return new Pew(target);
//            case "PC":
//            case "pc":
//                check pewcharge availability here??
//                return new PewCharge(target);
//                break;
            // Block
            case "b":
            case "B":
                return new Block();
            // Doesn't fit a shortcut
            default:
                throw new IllegalArgumentException("Invalid shortcut for a Move");
        }
    }

    public void resetStats() {
        attack = 0;
        defense = 0;
        move = null;
        target = null;
    }

    public void resetAll() {
        attack = 0;
        defense = 0;
        chargeCount = 0;
        blockCount = 0;
        doubleCount = 0;
        smokeCount = 0;
        move = null;
        target = null;
        alive = true;
        havePewCharge = true;
        name = "";
    }

    public void setMove(Move move) {
        this.move = move;
    }

    public Move getMove() {
        return move;
    }

    public String getName() {
        return name;
    }

    public void addCharge() {
        chargeCount++;
    }


    public void addBlock() {
        blockCount++;
    }

    public void addDouble() {
        doubleCount++;
    }


    public void addSmoke() {
        smokeCount++;
    }

    public int charges() {
        return chargeCount;
    }

    public int blocks() {
        return blockCount;
    }

    public int doubles() {
        return doubleCount;
    }

    public int smokes() {
        return smokeCount;
    }

    public Player getTarget() {
        return target;
    }
}
