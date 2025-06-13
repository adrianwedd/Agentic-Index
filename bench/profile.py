import cProfile
from pathlib import Path

from bench.benchmark import run


def main() -> None:
    prof = cProfile.Profile()
    prof.enable()
    run()
    prof.disable()
    out = Path("bench/profile.prof")
    out.parent.mkdir(exist_ok=True)
    prof.dump_stats(str(out))
    print(f"Profile written to {out}")
    try:
        import snakeviz
        snakeviz.main([str(out)])
    except Exception as exc:
        print(f"snakeviz failed: {exc}")


if __name__ == "__main__":
    main()
