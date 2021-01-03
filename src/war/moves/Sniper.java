package war.moves;

import war.Player;

// TODO: GOES THROUGH SMOKE
public class Sniper extends Attack {
    public Sniper(Player target) {
        super("Sniper", new Resource.Resources[]{Resource.Resources.BLOCK, Resource.Resources.BLOCK}, target);
    }

    @Override
    public int damageOf() {
        return 1;
    }
}
