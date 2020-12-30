import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
    p, h1, h2, ion-icon {
        color: ${({ theme }) => theme.main_text};
    }

    body {
        background: ${({ theme }) => theme.main_bg};
    }

    header {
        background: ${({ theme }) => theme.header_bg};
        border-right-color: ${({ theme }) => theme.borders};
    }

    .main_content, body {
        background: ${({ theme }) => theme.main_bg};
    }

    .player {
        background: ${({ theme }) => theme.player_bg};
        border-top-color: ${({ theme }) => theme.borders};
        box-shadow: ${({ theme }) => theme.player_shadow};
    }
`