package war.moves;

import war.Player;

public abstract class Attack extends Move {
    int damage;
    Player target;

    public Attack(String type, Player target) {
        super(type);
        this.target = target;
        damage = damageOf();
    }

    abstract public int damageOf();
}
