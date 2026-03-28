import time
import os
import numpy as np
import face_recognition
import multiprocessing


KNOWN_IMAGE_PATH = "activity1_4/known_man.jpg"
IMAGESET_PATH    = "activity1_4/imageset/"
TOLERANCE        = 0.6  # L2 distance threshold used by face_recognition internally


def check_image(args):
    """
    Worker function: loads one image and checks whether any face in it
    matches the known encoding.

    Returns the filename string if a match is found, otherwise None.
    Each worker process loads only its own image, keeping memory use low.
    """
    filepath, known_encoding = args

    unknown_image     = face_recognition.load_image_file(filepath)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        # numpy L2 norm — identical to the distance metric used by
        # face_recognition.compare_faces internally, but called directly
        # so we stay in numpy without the extra Python-level wrapper call.
        distance = np.linalg.norm(known_encoding - np.array(unknown_encoding))
        if distance < TOLERANCE:
            return os.path.basename(filepath)

    return None


if __name__ == "__main__":
    start = time.time()

    # Load the known face once in the main process; workers receive only
    # the 128-element numpy array (not the full image), minimising IPC data.
    known_image    = face_recognition.load_image_file(KNOWN_IMAGE_PATH)
    known_encoding = np.array(face_recognition.face_encodings(known_image)[0])

    filenames = [
        os.path.join(IMAGESET_PATH, f.name)
        for f in os.scandir(IMAGESET_PATH)
        if f.is_file()
    ]

    # One worker per logical CPU for true parallelism across processes.
    num_workers = multiprocessing.cpu_count()
    args = [(fp, known_encoding) for fp in filenames]

    match_found = None
    with multiprocessing.Pool(processes=num_workers) as pool:
        # imap_unordered yields results as soon as any worker finishes,
        # so we can stop immediately when the match is found rather than
        # waiting for all 120 images to be processed.
        for result in pool.imap_unordered(check_image, args):
            if result is not None:
                match_found = result
                pool.terminate()  # cancel remaining work immediately
                break

    if match_found:
        print(f"Match found! in {match_found}")
    else:
        print("No match found.")

    print(f"Time: {time.time() - start:.4f}s")
