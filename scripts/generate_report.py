import os
import sys

def generate_report(output_folder):
    frames_folder = os.path.join(output_folder, 'frames')
    detected_folder = os.path.join(output_folder, 'detected')
    faces_folder = os.path.join(output_folder, 'faces')
    actions_folder = os.path.join(output_folder, 'actions')

    report = []

    # Summarize frame processing
    total_frames = len(os.listdir(frames_folder))
    report.append(f"Total frames processed: {total_frames}")

    # Summarize detected players
    total_detected = len(os.listdir(detected_folder))
    report.append(f"Total frames with detected players: {total_detected}")

    # Summarize face recognition
    total_faces = len(os.listdir(faces_folder))
    report.append(f"Total frames with recognized faces: {total_faces}")

    # Summarize actions
    total_actions = len(os.listdir(actions_folder))
    report.append(f"Total frames with recognized actions: {total_actions}")

    # Detailed action summary
    action_summary = {}
    for action_file in os.listdir(actions_folder):
        with open(os.path.join(actions_folder, action_file)) as f:
            actions = f.readlines()
            for action in actions:
                action = action.strip()
                if action not in action_summary:
                    action_summary[action] = 0
                action_summary[action] += 1

    report.append("Action summary:")
    for action, count in action_summary.items():
        report.append(f"{action}: {count}")

    # Print the report
    for line in report:
        print(line)

if __name__ == "__main__":
    output_folder = sys.argv[1]
    generate_report(output_folder)
