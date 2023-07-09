def nms_modified(boxes, scores, classes, hierarchy, score_threshold, iou_threshold):

    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    selected_boxes = []

    while len(sorted_indices) > 0:

        best_index = sorted_indices[0]
        best_box = boxes[best_index]
        best_class = classes[best_index]

        if scores[best_index] < score_threshold:
            break

        selected_boxes.append((best_box, scores[best_index], best_class))

        sorted_indices = sorted_indices[1:]

        overlapping_indices = []

        for index in sorted_indices:
            box = boxes[index]
            box_class = classes[index]

            iou = compute_iou(best_box, box)

            if best_class == box_class:
                if iou > iou_threshold:
                    overlapping_indices.append(index)
            else:
                if is_parent(box_class, best_class, hierarchy):
                    if iou > iou_threshold:
                        overlapping_indices.append(index)

        sorted_indices = [index for index in sorted_indices if index not in overlapping_indices]

    return selected_boxes

def compute_iou(box1, box2):

    xmin = max(box1[0], box2[0])
    ymin = max(box1[1], box2[1])
    xmax = min(box1[2], box2[2])
    ymax = min(box1[3], box2[3])
    intersection_area = max(0, xmax - xmin) * max(0, ymax - ymin)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - intersection_area

    iou = intersection_area / union_area if union_area > 0 else 0
    
    return iou

def is_parent(child_class, parent_class, hierarchy):
    if parent_class in hierarchy.get(child_class, []):
        return True

    for ancestor in hierarchy.get(child_class, []):
        if is_parent(ancestor, parent_class, hierarchy):
            return True

    return False


def main():
    boxes = [
        [10, 20, 50, 60],    # Box 0
        [15, 25, 55, 65],    # Box 1
        [40, 50, 80, 90],    # Box 2
        [45, 55, 85, 95],    # Box 3
        [70, 80, 110, 120],  # Box 4
    ]

    scores = [0.9, 0.8, 0.7, 0.85, 0.95]
    classes = ['Apple', 'Apple', 'Fruit', 'Fruit', 'Fruit']
    hierarchy = {'Apple': ['Fruit']}
    score_threshold = 0.8
    iou_threshold = 0.5

    # Testing the NMS algorithm
    selected_boxes = nms_modified(boxes, scores, classes, hierarchy, score_threshold, iou_threshold)

    for box, score, class_label in selected_boxes:
        print("Box:", box, "Score:", score, "Class:", class_label)

if __name__ == '__main__':
    main()