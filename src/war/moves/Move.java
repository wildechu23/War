package war.moves;

public abstract class Move {
    String type;

    public Move(String type) {
        this.type = type;
    }

    public String getType() {
        return type;
    }
}



/*
// Type, Cost, CostType, Attack, Defense, Charges, Blocks, Doubles, Smokes

    // TODO: Implement:
    One charge or one block a turn
    Smoke
    Sniper through Smoke
    GhostGun losing to any gun, but killing with 0 dmg

*/
