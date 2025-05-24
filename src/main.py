from src.models.world import World


def main():
    world = World()

    max_ticks = 10
    results = {}
    for tick in range(1, max_ticks + 1):
        data = world.tick(tick)
        results[tick] = data

    print(results)


if __name__ == "__main__":
    main()
