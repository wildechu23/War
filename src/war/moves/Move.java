package war.moves;

public abstract class Move {
    private String type;
    private Resource.Resources[] cost;

    public Move(String type, Resource.Resources[] cost) {
        this.type = type;
        this.cost = cost;
    }

    public String getType() {
        return type;
    }
    public Resource.Resources[] getCost() { return cost; }

    @Override
    public String toString() {
        return type;
    }
}



/*
// Type, Cost, CostType, Attack, Defense, Charges, Blocks, Doubles, Smokes

    // TODO: Implement:
    Smoke
    Sniper through Smoke
    SmokeMachine
    Reflect
    GhostGun losing to any gun, but killing with 0 dmg
    GhostGun goes through Smoke
*/
