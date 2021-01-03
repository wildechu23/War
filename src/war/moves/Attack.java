package war.moves;

import war.Player;

public abstract class Attack extends Move {
    int damage;
    Player target;

    public Attack(String type, Resource.Resources[] cost, Player target) {
        super(type, cost);
        this.target = target;
        damage = damageOf();
    }

    abstract public int damageOf();
}
