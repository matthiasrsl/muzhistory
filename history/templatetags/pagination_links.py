from django import template

register = template.Library()


@register.inclusion_tag("history/pagination_links.html")
def page_links(paginator, current, view_name, suffix="?page="):
    """
    Tags that displays links to the intelligently choosen pages.
    """
    num_pages = paginator.num_pages
    current = int(current)
    page_numbers = [current]
    for num in [1, 2, current - 1, current + 1, num_pages, num_pages - 1]:
        if num not in page_numbers and num > 0 and num <= num_pages:
            page_numbers.append(num)
            page_numbers.sort()

    new_page_numbers = [page_numbers[0]]
    j = 1
    for i in range(1, len(page_numbers)):
        if (page_numbers[i] - page_numbers[i-1] > 1):
            new_page_numbers.append(0)
        new_page_numbers.append(page_numbers[i])
    page_numbers = new_page_numbers

    return {
        "page_numbers": page_numbers,
        "current": current,
        "view_name": view_name,
        "suffix": suffix,
    }
