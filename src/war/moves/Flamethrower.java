package war.moves;

import war.Player;

public class Flamethrower extends Attack {
    public Flamethrower(Player target) {
        super("Flamethrower", new Resource.Resources[]{Resource.Resources.CHARGE, Resource.Resources.CHARGE}, target);
    }

    @Override
    public int damageOf() {
        return 2;
    }
}
