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

    public ArrayList<Move> inputMove() {
        boolean isAttack = false;
        boolean isResource = false;
        Scanner s = new Scanner(System.in);
        System.out.println("Enter Moves");
        String input = s.nextLine();
        String[] inputList = input.split(" "); // split by spaces
        // if inputMove is Attack, ask target
        ArrayList<Move> moves = new ArrayList<Move>();
        for(String i : inputList) {
            Move move = parseInput(i);
            // isAttack
            if(!isAttack && move instanceof Attack) {
                isAttack = true;
            }
            // checkValidity in different method
            if(checkValidity(move, isAttack, isResource, havePewCharge)) {
                moves.add(move);
            }
            // isResource
            if(!isResource && move instanceof Resource && !(move instanceof PewCharge)) {
                isResource = true;
            }
            // havePewCharge
            if(move instanceof PewCharge) {
                havePewCharge = false;
            }
        }
        return moves;
    }

    // TODO: Don't throw error, just reask
    public boolean checkValidity(Move move, boolean isAttack, boolean isResource, boolean havePewCharge) {
        if(!havePewCharge) {
            if(move instanceof PewCharge) {
                throw new IllegalArgumentException("One PewCharge per game");
            }
        }
        if(isAttack) {
            if(!(move instanceof Attack)) {
                throw new IllegalArgumentException("If attacking, all moves must be attacks");
            }
        }
        if(isResource) {
            throw new IllegalArgumentException("Can only do one move if resource");
        }
        return true;
    }

    // read input, should be in form BA P PC = Bazooka Pew PewCharge, caps doesn't matter
    public Move parseInput(String string) {
        switch(string) {
            // Charge
            case "c":
            case "C":
                return new Charge();
            // Pew
            case "p":
            case "P":
                return new Pew(target);
            // PewCharge
            case "pc":
            case "PC":
                return new PewCharge(target);
            // Block
            case "b":
            case "B":
                return new Block();
            //Bazooka
            case "ba":
            case "BA":
                return new Bazooka(target);
            //Sniper
            case "sn":
            case "SN":
                return new Sniper(target);
            // FlameThrower
            case "fl":
            case "FL":
                return new Flamethrower(target);
            // Double
            case "db":
            case "DB":
                return new war.moves.Double();
            // Unbreakable
            case "un":
            case "UN":
                return new Unbreakable(target);
            // Bionic
            case "bi":
            case "BI":
                return new Bionic();
            // Doesn't fit a shortcut
            default:
                // TODO: Handle properly, don't just throw error but ask again
                throw new IllegalArgumentException("Invalid shortcut for a Move: " + string);
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

    public String listResources() {
        return "Charges: " + charges() + "\n" +
                "Blocks: " + blocks() + "\n" +
                "Doubles: " + doubles() + "\n" +
                "Smokes: " + smokes() + "\n";
    }

    public Player getTarget() {
        return target;
    }
}
