package war.moves;

import war.Player;

public class Bazooka extends Attack {
    public Bazooka(Player target) {
        super("Bazooka", new Resource.Resources[]{Resource.Resources.BLOCK, Resource.Resources.BLOCK}, target);
    }

    @Override
    public int damageOf() {
        return 2;
    }
}
