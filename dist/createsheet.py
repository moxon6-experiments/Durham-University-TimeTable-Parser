from parse_timetable import get_schedule_items
from utils import get_days
from excel_autofit import auto_fit_columns
from utils import clear
import xlwt


def organise_by_module(tutorials):
    """
    Takes a list of Tutorial Schedule Objects and
    returns a dictionary of module:tutorial
    """
    tutorial_dict = {}
    for tutorial in tutorials:
        if tutorial.module_code not in tutorial_dict:
            tutorial_dict[tutorial.module_code] = [tutorial]
        else:
            tutorial_dict[tutorial.module_code].append(tutorial)
    return tutorial_dict


def manage_tutorials(tutorials):
    """
    Takes a list of Tutorial Schedule Objects,
    asks the user which tutorials are applicable
    and returns this subset list of tutorials
    """
    tutorial_dict = organise_by_module(tutorials)
    sorted_tutorials = tutorial_dict.values()
    tutorials_out = set()
    for module in sorted_tutorials:
        module.sort(key=lambda y: [y.day_number, y.time_hour])
        clear()
        verifying = True
        while verifying:
            print "Please Input Values (comma separated) of the Non-Lecture Items that Apply to You"
            print_outs = []
            for tutorial in module:
                if tutorial.to_string() not in print_outs:
                    print str(module.index(tutorial)+1)+"."+tutorial.to_string()
                    print_outs.append(tutorial.to_string())
            string_values = get_input("Input Values:")
            try:
                values = [int(x) for x in string_values.split(",")]
                verifying = False
                for x in values:
                    tutorials_out.add(module[x-1])
            except:
                print "InputError:"
                print string_values
                print "Invalid Input, try again"
                verifying = True
    return list(tutorials_out)


def create_timetable(module_list, details):
    """
    Takes a list of module code strings and an array of
    [username,password], and generates a spreadsheet file
    corresponding to the weekly timetable of that user
    """
    schedule_items = get_schedule_items(module_list, details)
    lectures = []
    tutorials = []
    for schedule_item in schedule_items:
        if schedule_item.schedule_type == "LECT":
            lectures.append(schedule_item)
        else:
            tutorials.append(schedule_item)
    tutorials = manage_tutorials(tutorials)
    schedule_items = lectures + tutorials
    schedule_items = check_clashes(schedule_items)
    make_spreadsheet(schedule_items)
    return schedule_items


def check_clashes(schedule_items):
    """
    Iterates through schedule objects currently registered
    and checks which weeks those schedule objects clash (if any).
    For each week that the two clash, ask the user which item to keep
    """
    clear()
    for comp1 in schedule_items:
        for comp2 in schedule_items:
            clash_weeks = comp1.clash(comp2)
            if clash_weeks is not None:
                for week in clash_weeks:
                    print "TimeTable Clash on week: %s" % str(week)
                    print "1." + comp1.to_string()[0,2:]
                    print "2." + comp2.to_string()[0,2:]
                    keep = get_input("Input Item to Keep: ")
                    if keep[0] + " " == "1":
                        comp2.weeks.remove(week)
                    else:
                        comp1.weeks.remove(week)
    clear()
    return schedule_items


def make_spreadsheet(schedule_items):
    workbook, worksheets = get_default_book()
    styles = {
        1: get_color_style('red'),
        2: get_color_style('light_orange'),
        3: get_color_style('yellow'),
        4: get_color_style('bright_green'),
        5: get_color_style('ocean_blue'),
        6: get_color_style('violet')
        }
    for schedule_item in schedule_items:
        for week in schedule_item.weeks:
            try:
                worksheets[week].write(schedule_item.time_hour+1,
                                       schedule_item.day_number+1,
                                       schedule_item.module_name,
                                       styles[schedule_item.module_number])
            except Exception, e:
                clear()
                print str(e)
                print schedule_item.to_string()
                get_input('')
            if schedule_item.duration != 1:
                worksheets[week].merge(schedule_item.time_hour+1,
                                       schedule_item.time_hour+schedule_item.duration,
                                       schedule_item.day_number+1,
                                       schedule_item.day_number+1)
    try:
        file_name = get_input('Input File Output name: ')
        file_name = file_name.replace(".xlsx", "")
        file_name = file_name.replace(".xls", "")
        file_name = file_name.split(".")[0]
        file_name += ".xls"
        workbook.save(file_name)
        try:
            auto_fit_columns(file_name)
        except Exception, e:
            print "AutoFitting Columns Failed"
            print str(e)

    except Exception, e:
        print str(e)


def get_default_style():
    style = xlwt.XFStyle()
    # borders
    borders = xlwt.Borders()
    borders.left = borders.right = borders.top = borders.bottom = xlwt.Borders.THIN
    style.borders = borders
    return style


def get_color_style(color):
    style = get_default_style()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[color]
    style.pattern = pattern
    return style


def get_default_book(weeks=range(11, 53)):
    style = get_default_style()
    workbook = xlwt.Workbook()
    worksheets = {}
    for sheet_number in weeks:
        worksheets[sheet_number] = workbook.add_sheet('Week %s' % sheet_number, cell_overwrite_ok=True)
        days = get_days()
        for x in range(1, 6):
            worksheets[sheet_number].write(1, x + 1, days[x], style)
        for y in range(2, 12):
            time = "0" * (2 - len(str(y + 7))) + str(y + 7) + ":00"
            worksheets[sheet_number].write(y, 1, time, style)
        for y in range(2, 7):
            for x in range(2, 12):
                worksheets[sheet_number].write(x, y, "", style)
    return workbook, worksheets


def main():
    modules_string = get_input("""Input Comma Separated
                            module codes of the modules \n
                            you wish to generate a timetable for \n
                            Modules:""")
    module_list = modules_string.split(",")
    username = get_input("Username:")
    password = get_input('Password')
    create_timetable(module_list, [username, password])


def get_input(message):
    try:
        x = raw_input(message)
        return x
    except:
        raise SystemExit


if __name__ == "__main__":
    main()
