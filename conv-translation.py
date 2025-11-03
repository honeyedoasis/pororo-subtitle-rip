import json


def get_settings():
    with open('settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    settings = get_settings()
    my_project_id = settings['project_name']

    with open(f'gemini/{my_project_id}.srt', encoding='utf-8-sig') as timings_file:
        timings_lines = timings_file.read().split('\n\n')

    timings = dict()
    for i, t in enumerate(timings_lines):
        lines = t.split('\n')
        if len(lines) > 1:
            num = lines[0]

            if i + 1 != int(num):
                print('WTF', i + 1, int(num))
                breakpoint()

            timing = lines[1]
            timings[num] = timing
            # print(num, '\t', timing)
        else:
            print('Line too short line', i)

    with open(f'gemini/{my_project_id}.gemini', encoding='utf-8-sig') as gemini_file:
        translation = gemini_file.read().split('\n\n')

    out = ''

    for i, t in enumerate(translation):
        lines = t.split('\n')
        if len(lines) > 1:
            num = lines[0]
            # num = str(i + 1)
            translation = '\n'.join(lines[1:])
            timing = timings[num]

            out += num + '\n' + timing + '\n' + translation + '\n\n'

            if str(i + 1) != num:
                print('Bad', i , num)
        else:
            print('Invalid line', i)
            #
            # print(num)
            # print(timing)
            # print(translation + '\n')
        # else:
        #     print('WTF')
        #     print(lines)
        #     breakpoint()
            # print(timing)
            # print(translation + '\n')
            # if len(translation) == 0:
            #     breakpoint()
            # print('\n')
    # print(translation)
    with open(f'gemini/{my_project_id}.en.srt', 'w', encoding='utf-8') as out_file:
        out_file.write(out)


if __name__ == "__main__":
    main()
