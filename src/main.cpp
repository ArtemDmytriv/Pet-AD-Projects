#include <SFML/Graphics/RenderWindow.hpp>
#include <iostream>

#include "Game.hpp"

int main() {

    game::Game inst{};

    inst.run();

    return 0;
}
