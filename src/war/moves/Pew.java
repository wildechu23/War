package war.moves;

import war.Player;

public class Pew extends Attack {
    public Pew(Player target) {
        super("Pew", new Resource.Resources[]{Resource.Resources.CHARGE}, target);
    }

    @Override
    public int damageOf() {
        return 1;
    }

    @Override
    public String toString() {
        return "p";
    }
}
