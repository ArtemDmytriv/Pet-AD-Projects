#include "Game.hpp"
#include <SFML/Graphics/Color.hpp>
#include <SFML/System/Clock.hpp>
#include <SFML/System/Time.hpp>
#include <SFML/System/Vector3.hpp>
#include <SFML/Window/Event.hpp>

#include <iostream>

namespace game {

Game::Game()
    : mWindow{sf::VideoMode(640, 480), "SFML Application"}, mTexture{},
      mPlayer{}, move{} {

    if (!mTexture.loadFromFile("sprites/spaceship-birds-eye-view.png")) {
        std::cerr << "No texture file";
        exit(-1);
    }

    mPlayer.setTexture(mTexture);
    mPlayer.setPosition(100.f, 100.f);
    mPlayer.setScale(.25f, .25f);
    mPlayer.setRotation(90);
}

Game::~Game() { mWindow.close(); }

void Game::run() {
    sf::Clock clock;
    sf::Time timeSinceLastUpdate = sf::Time::Zero;
    while (mWindow.isOpen()) {
        timeSinceLastUpdate += clock.restart();
        while (timeSinceLastUpdate > TimePerFrame) {
            timeSinceLastUpdate -= TimePerFrame;
            processEvents();
            update(TimePerFrame);
        }
        render();
    }
}

void Game::processEvents() {
    sf::Event event;
    while (mWindow.pollEvent(event)) {
        switch (event.type) {
        case sf::Event::KeyPressed:
            handlePlayerInput(event.key.code, true);
            break;
        case sf::Event::KeyReleased:
            handlePlayerInput(event.key.code, false);
            break;
        case sf::Event::Closed:
            mWindow.close();
            break;
        default:
            break;
        }
    }
}

void Game::handlePlayerInput(sf::Keyboard::Key key, bool isPressed) {
    switch (key) {
    case sf::Keyboard::W:
        move.up = isPressed;
        break;
    case sf::Keyboard::S:
        move.down = isPressed;
        break;
    case sf::Keyboard::A:
        move.left = isPressed;
        break;
    case sf::Keyboard::D:
        move.right = isPressed;
        break;
    default:
        break;
    }
}

void Game::update(sf::Time deltaTime) {
    sf::Vector2f movement(0.f, 0.f);
    float scalar = 30.f;
    if (move.up)
        movement.y -= scalar;
    if (move.down)
        movement.y += scalar;
    if (move.left)
        movement.x -= scalar;
    if (move.right)
        movement.x += scalar;

    mPlayer.move(movement * deltaTime.asSeconds());
}

void Game::render() {
    mWindow.clear();
    mWindow.draw(mPlayer);
    mWindow.display();
}

} // namespace game
