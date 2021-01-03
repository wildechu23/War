package war.moves;

import war.Player;

public class Unbreakable extends Attack {
    public Unbreakable(Player target) {
        super("Unbreakable", new Resource.Resources[]{Resource.Resources.DOUBLE}, target);
    }

    @Override
    public int damageOf() {
        return 2;
    }
}
