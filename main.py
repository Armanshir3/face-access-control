"""Command-line entry point for the Face Recognition Access Control System."""

import argparse

from src import access_control, capture_faces, train_model


def main():
    parser = argparse.ArgumentParser(
        description="Real-Time Face Recognition Access Control System"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_parser = subparsers.add_parser("register", help="Enroll a new user")
    register_parser.add_argument("name", help="Name of the user to enroll")

    subparsers.add_parser("train", help="Train the recognition model")
    subparsers.add_parser("run", help="Start the access control system")

    args = parser.parse_args()

    if args.command == "register":
        capture_faces.capture_user(args.name)
    elif args.command == "train":
        train_model.train()
    elif args.command == "run":
        access_control.run()


if __name__ == "__main__":
    main()
