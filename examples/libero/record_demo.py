# examples/libero/record_demo.py
import os
import pathlib
import importlib.util

# ---- 可按需修改/用环境变量覆盖 ----
HOST = os.getenv("OPENPI_HOST", "127.0.0.1")
PORT = int(os.getenv("OPENPI_PORT", "8000"))
OUT_DIR = os.getenv("OUT_DIR", "./rollouts")         # 视频输出目录
TASK_SUITE = os.getenv("TASK_SUITE", "libero_spatial")
TRIALS_PER_TASK = int(os.getenv("TRIALS_PER_TASK", "1"))  # 每个任务跑多少条（默认 1）
RESIZE = int(os.getenv("RESIZE", "224"))
REPLAN_STEPS = int(os.getenv("REPLAN_STEPS", "5"))
SEED = int(os.getenv("SEED", "7"))
# -----------------------------------

def load_main_module():
    here = pathlib.Path(__file__).resolve()
    main_path = here.parent / "main.py"
    if not main_path.exists():
        raise FileNotFoundError(f"未找到 main.py: {main_path}")
    spec = importlib.util.spec_from_file_location("libero_example_main", str(main_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    mod = load_main_module()          # 动态加载 examples/libero/main.py
    Args = mod.Args                   # 取出 dataclass Args
    eval_libero = mod.eval_libero     # 取出主入口

    args = Args(
        host=HOST,
        port=PORT,
        resize_size=RESIZE,
        replan_steps=REPLAN_STEPS,
        task_suite_name=TASK_SUITE,
        num_steps_wait=10,
        num_trials_per_task=TRIALS_PER_TASK,
        video_out_path=OUT_DIR,
        seed=SEED,
    )

    # 确保输出目录存在
    pathlib.Path(args.video_out_path).mkdir(parents=True, exist_ok=True)

    print(f"[INFO] running eval_libero with server ws://{args.host}:{args.port}")
    print(f"[INFO] videos will be saved to: {args.video_out_path}")
    eval_libero(args)

if __name__ == "__main__":
    # 无显示环境务必设置
    if os.getenv("MUJOCO_GL") is None:
        os.environ["MUJOCO_GL"] = "egl"
    main()
