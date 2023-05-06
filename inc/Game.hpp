#pragma once

#include <SFML/Graphics.hpp>
#include <SFML/Graphics/CircleShape.hpp>
#include <SFML/Graphics/RenderWindow.hpp>
#include <SFML/Graphics/Sprite.hpp>
#include <SFML/Graphics/Texture.hpp>
#include <SFML/System/Time.hpp>
#include <SFML/Window.hpp>
#include <SFML/Window/Keyboard.hpp>

#include <iosfwd>

namespace game {

class Game {
  public:
    Game();
    ~Game();

    void run();

  private:
    const sf::Time TimePerFrame = sf::seconds(1.f / 120.f);

    void processEvents();

    void handlePlayerInput(sf::Keyboard::Key key, bool isPressed);

    void update(sf::Time deltaTime);

    void render();

    sf::RenderWindow mWindow;

    sf::Texture mTexture;
    sf::Sprite mPlayer;

    struct Movement {
        bool up;
        bool down;
        bool left;
        bool right;
        void print(std::ostream &out) {
            out << "U:D:L:R (" << up << ':' << down << ':' << left << ':'
                << right << ")\n";
        }
    } move;
};

} // namespace game
